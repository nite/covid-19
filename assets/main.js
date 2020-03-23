function getElementByClass(className, element = document) {
    return element.getElementsByClassName(className)[0];
}

function triggerRelayout(delay) {
    if (delay) {
        setTimeout(() => triggerRelayout(), 100);
    } else {
        window.dispatchEvent(new Event('resize'));
    }
}

function relayoutViz() {
    const mainContent = getElementByClass('main-content');
    console.log('sidebar toggle');
    mainContent.style['overflow-x'] = 'hidden';
    setTimeout(() => {
        triggerRelayout();
        setTimeout(() => mainContent.style['overflow-x'] = 'visible');
    });
}

function collapse(plot, icon) {
    if (!plot['dimensions']) {
        return;
    }

    icon.classList.remove('fa-compress');
    icon.classList.add('fa-expand');
    const dimensions = plot['dimensions'];
    delete plot['dimensions'];
    plot.classList.remove('maximised');
    let [width, height] = dimensions;
    plot.style['width'] = (width - 10) + 'px';
    plot.style['height'] = (height - 10) + 'px';
    plot.style['max-width'] = width + 'px';
    plot.style['max-height'] = height + 'px';
    setTimeout(() => {
        triggerRelayout();
        setTimeout(() => {
            plot.style['width'] = plot.style['height'] = plot.style['max-width'] = plot.style['max-height'] = '';
        }, 100)
    }, 100);

    if (escCollapseHandler) {
        window.removeEventListener('keyup', escCollapseHandler);
        escCollapseHandler = undefined;
    }
}

function toggleExpandViz(targetElement) {
    if (!(targetElement.classList.contains('fa-expand') || targetElement.classList.contains('fa-compress'))) {
        return;
    }
    let icon = targetElement;
    const plot = icon.parentNode;
    if (plot['dimensions']) {
        collapse(plot, icon);
    } else {
        plot['dimensions'] = [plot.offsetWidth, plot.offsetHeight];
        escCollapseHandler = e => {
            if (e.keyCode === 27) {
                setTimeout(() => collapse(plot, icon));
            }
        };
        window.addEventListener('keyup', escCollapseHandler);
        icon.classList.add('fa-compress');
        icon.classList.remove('fa-expand');
        plot.classList.add('maximised');
        triggerRelayout(true);
    }
}

let wiredUp = false

function wireupMaximisers() {
    if (wiredUp) {
        return;
    }
    setTimeout(() => {
        if (wiredUp) {
            return;
        }
        const elements = [...document.getElementsByClassName('fa-expand')];
        if (elements.length) {
            elements.forEach(el => {
                el.addEventListener(
                    'click',
                    event => toggleExpandViz(event.target));
            })
            wiredUp = true;
        } else {
            wireupMaximisers();
        }

    }, 100)
}

wireupMaximisers();
