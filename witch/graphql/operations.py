import sgqlc.types
import sgqlc.operation
import twitch_sgqlc

__all__ = ('Operations',)


def query_get_live_user():
    _op = sgqlc.operation.Operation(twitch_sgqlc.schema.query_type, name='GetLiveUser', variables=dict(login=sgqlc.types.Arg(sgqlc.types.non_null(twitch_sgqlc.schema.String))))
    _op_user = _op.user(login=sgqlc.types.Variable('login'))
    _op_user.login()
    _op_user.display_name()
    _op_user.description()
    _op_user_roles = _op_user.roles()
    _op_user_roles.is_partner()
    _op_user_broadcast_settings = _op_user.broadcast_settings()
    _op_user_broadcast_settings.title()
    _op_user_broadcast_settings_game = _op_user_broadcast_settings.game()
    _op_user_broadcast_settings_game.box_art_url()
    _op_user_broadcast_settings_game.name()
    _op_user_broadcast_settings.is_mature()
    _op_user_stream = _op_user.stream()
    _op_user_stream_tags = _op_user_stream.tags()
    _op_user_stream_tags.localized_name()
    _op_user_stream_tags.localized_description()
    _op_user_stream_tags.id()
    _op_user_stream.created_at()
    _op_user_stream.preview_image_url(width=1920, height=1080)
    _op_user_stream_playback_access_token = _op_user_stream.playback_access_token(params={'platform': 'web', 'playerBackend': 'mediaplayer', 'playerType': 'site'})
    _op_user_stream_playback_access_token.signature()
    _op_user_stream_playback_access_token.value()
    _op_user_stream.viewers_count()
    return _op


class Query:
    get_live_user = query_get_live_user()


class Operations:
    query = Query
