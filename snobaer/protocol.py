#!/usr/bin/env python
# encoding: utf-8

"""Protocol definiton which is used between this backend and the frontend. This
only describes the data which is exchanged on the websocket. We try to keep
this as small as possible in order to reduce complexity in the frontend.

The data format is json due to the easy parsing on client side.

General Message format:

    {
        'type': (cmd|info)
        'name': [cmd]
        'params': [p1, p2, p3, ...]
    }

Client -> Server types:
=======================

mpd
---

* [actual_command]   # See moose-mpd-client.c:1030 for [actual_command]
* close              # Close the connection from client.

store
-----

* query-queue [query]
* query-database [query]
* query-directories [depth] [query]
* query-spl [name] [query]

Server -> Client types:
=======================

* status            # include MooseStatus and MooseSong
* outputs           # list of MooseOutputs
* playlist          # json list of of MooseSongs with context id

"""

# Stdlib:
import json
import logging

LOGGER = logging.getLogger('proto')

# External:
from gi.repository import Moose

###############
#  UTILITIES  #
###############

def copy_header(document):
    return {
        'type': document['type'],
        'detail': document['detail']
    }

########################
#   SERVER -> CLIENT   #
########################


def serialize_song(song):
    if song is None:
        return {}

    # Only serialize the most needed data for now.
    keys = ['artist', 'album', 'title', 'id']
    return {key: getattr(song.props, key) for key in keys}


def serialize_state(state):
    # This cast is for safety.
    return Moose.State(state).value_nick


def serialize_status(status, event=None, detail='timer'):
    # Just serialize all the status data
    status_data = {
        'type': 'status',
        'detail': detail,
        'status': {
            i.name: status.get_property(i.name) for i in Moose.Status.props
        }
    }

    status_data['status']['events'] = Moose.Idle(event).value_nicks if event else []

    print(status.get_current_song())
    status_data['status']['state'] = serialize_state(status.props.state)
    status_data['status']['song'] = serialize_song(status.get_current_song())
    return status_data


def serialize_playlist(playlist, detail='queue'):
    return {
        'type': 'playlist',
        'detail': detail,
        'songs': [serialize_song(song) for song in playlist]
    }

########################
#   CLIENT -> SERVER   #
########################


def _parse_mpd_command(client, document, callback):
    client.send(document['detail'])


def _parse_store_command(client, document, callback):
    # TODO: Moosecat supports asynchronous queries,
    #       so make this return a future.
    detail = document['detail']
    query = document['query']

    if detail == 'queue':
        playlist = client.store.query_sync(query, queue_only=True)
    elif detail == 'database':
        playlist = client.store.query_sync(query, queue_only=False)
    elif detail == 'stored':
        playlist_name = document['playlist_name']
        # TODO
    elif detail == 'directories':
        pass
        # TODO

    song_list = []
    response = copy_header(document)
    response['target'] = document.get('target')
    response['songs'] = song_list

    for song in playlist:
        song_list.append(serialize_song(song))

    callback(response)


def _parse_metadata_command(client, document, callback):
    query = Moose.MetadataQuery(
        type=document.get('get_type'),
        artist=document.get('artist'),
        album=document.get('album'),
        title=document.get('title'),
        download=False
    )

    def _done(_, query):
        response = copy_header(document)
        response['urls'] = []

        for cache in query.get_results():
            metadata = cache.props.data.get_data()
            response['urls'].append(metadata.decode('utf-8'))

        callback(response)
        client.metadata.disconnect_by_func(_done)

    client.metadata.connect('query-done', _done)
    LOGGER.debug('Commited metadata query: ' + str(document))
    client.metadata.commit(query)


HANDLERS = {
    'metadata': _parse_metadata_command,
    'mpd': _parse_mpd_command,
    'store': _parse_store_command
}


def _parse_doc(client, document, callback):
    doc_type = document.get('type')
    detail = document.get('detail')

    # Valid documents have at least a type and detail.
    if doc_type is None or detail is None:
        LOGGER.error('document is malformed:\n' + str(document))
        return

    handler = HANDLERS.get(doc_type)
    if handler is None:
        LOGGER.error('No such handler type: ' + str(doc_type))
        return

    return handler(client, document, callback)


def parse_message(client, message, callback):
    try:
        return _parse_doc(client, json.loads(message), callback)
    except ValueError as err:
        LOGGER.error('Unable to parse json message:\n' + message + str(err))



if __name__ == '__main__':
    import time

    client = Moose.Client.new(Moose.Protocol.DEFAULT)
    client.connect_to()
    client.force_sync(Moose.Idle(0xffffffff))
    time.sleep(0.5)
    client.wait()

    with client.reffed_status() as status:
        print(json.dumps(serialize_status(status), indent=4))