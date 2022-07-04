# mkdocs Material

When I first started the project, I used [GitHub Wiki](https://github.com/valhuber/ApiLogicServer/wiki) for docs.  It worked, but... meh.  In particular, combining site and page navigation into 1 tree on the right obscured the organization of the docs... and product.  That's a serious problem.

I was delighted to discover [GitHub Docs](https://docs.github.com/en) where you can build a minimal web site of static pages.

But what really made it work was the addition of [mkdocs-material](https://squidfunk.github.io/mkdocs-material/getting-started/), which is now the basis for the current docs.  It enabled me to define navigation (the left tree), and automitically creates the table of contents on the right.  I think you'll agree the transformation was magical.

It was not to hard to set up, since my pages were all markdown.  Hightlights, to perhaps save you some time:

1. Create a [docs folder]