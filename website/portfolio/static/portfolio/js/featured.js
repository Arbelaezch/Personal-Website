// Marks which featured project is showing. The page works without this file: each item links
// to its panel and the stylesheet shows the targeted one. This only adds the "current" highlight.
const links = [...document.querySelectorAll('[data-featured-link]')];

function markCurrent() {
    const current = links.find((link) => link.hash === location.hash) || links[0];
    for (const link of links) {
        if (link === current) {
            link.setAttribute('aria-current', 'true');
        } else {
            link.removeAttribute('aria-current');
        }
    }
}

if (links.length) {
    markCurrent();
    addEventListener('hashchange', markCurrent);
}
