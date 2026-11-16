// Which featured project is showing. The page works without this file: each item links to its
// panel and the stylesheet shows the targeted one. With it, selecting never scrolls the page, the
// current item is marked, and orbit.js can ask for a selection ("featured:pick") and hear about
// one ("featured:selected").
const section = document.querySelector('.featured');

if (section) {
    const links = [...section.querySelectorAll('[data-featured-link]')];
    const panels = links.map((link) => document.getElementById(link.hash.slice(1)));

    function select(index) {
        links.forEach((link, i) => {
            if (i === index) {
                link.setAttribute('aria-current', 'true');
            } else {
                link.removeAttribute('aria-current');
            }
        });
        panels.forEach((panel, i) => panel.classList.toggle('is-current', i === index));
        section.dispatchEvent(new CustomEvent('featured:selected', { detail: { index } }));
    }

    function fromAddress() {
        return links.findIndex((link) => link.hash === location.hash);
    }

    links.forEach((link, index) => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            select(index);
        });
    });
    section.addEventListener('featured:pick', (event) => select(event.detail.index));
    addEventListener('hashchange', () => {
        if (fromAddress() >= 0) select(fromAddress());
    });

    section.classList.add('js-select');
    select(Math.max(0, fromAddress()));
}
