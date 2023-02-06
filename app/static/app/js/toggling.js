function device_tag_open(element) {
    document.getElementById('devices').classList.toggle('open');
    src_toggle(element, 'chevron-back-outline', 'chevron-down');
}

function values_tag_open(el){
    src_toggle(el, 'chevron-back-outline', 'chevron-down');
}

function src_toggle(el, val1, val2){
    if (el.src.search(val1) !== -1) {
        el.src = el.src.replace(val1, val2);
      } else {
        el.src = el.src.replace(val2, val1);
      }
}