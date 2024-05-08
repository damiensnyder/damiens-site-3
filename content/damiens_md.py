from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
from customblocks.utils import E, Markdown
import xml.etree.ElementTree as etree


SOUNDCLOUD_EMBED_URL = "https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{}&color=%23ff7700&auto_play=false&hide_related=true&show_comments=false&show_user=false&show_reposts=false&show_teaser=false&visual=true"


class DelInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element('del')
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class DelExtension(Extension):
    def extendMarkdown(self, md):
        DEL_PATTERN = r'~~(.*?)~~'  # like --del--
        md.inlinePatterns.register(DelInlineProcessor(DEL_PATTERN, md), 'del', 175)


def soundcloud_embed(ctx, embed_code):
    return E('.soundcloud-embed-wrapper',
        E('iframe', src=SOUNDCLOUD_EMBED_URL.format(embed_code))
    )


def audio_embed(ctx, **sources):
    return E('audio',
        controls=True,
        *[E('source', src=url if "://" in url else f"/static/{url}" if "/" in url else f"/static/songs/{url}", type=f"audio/{type}")
          for type, url in sources.items()]
    )


def summary_details(ctx, summary):
    return E('details',
             E('summary', summary),
             Markdown(ctx.content, ctx.parser))
