from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from customblocks.utils import E, Markdown
import re


SOUNDCLOUD_EMBED_URL = "https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{}&color=%23ff7700&auto_play=false&hide_related=true&show_comments=false&show_user=false&show_reposts=false&show_teaser=false&visual=true"


class CaptionProcessor(Treeprocessor):
    CAPTION_RE = re.compile(r'^caption: ')

    def run(self, root):
        for block in root.iter('p'):
            if self.CAPTION_RE.match(block.text):
                block.set('class', 'caption')
                block.text = block.text[9:]

class CaptionExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(
            CaptionProcessor(md),
            'caption_processor',
            50
        )
        md.registerExtension(self)


def soundcloud_embed(ctx, embed_code):
    return E('.soundcloud-embed-wrapper',
        E('iframe', src=SOUNDCLOUD_EMBED_URL.format(embed_code))
    )


def audio_embed(ctx, **sources):
    return E('audio',
        controls=True,
        *[E('source', src=f"/static/content/songs/{url}", type=f"audio/{type}")
          for type, url in sources.items()]
    )
