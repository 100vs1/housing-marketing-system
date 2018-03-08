class HmsUi{
    constructor() {

    }

    showModal(id) {
        $('#' + id).modal('show');
    }

    hideModal(id) {
        $('#' + id).modal('hide');
    }

    setWindow(elmnt, ctlBtn = null, flag = null) {
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        let windowHeader = elmnt.getElementsByClassName('window-header')[0];
        let closeBtn = elmnt.getElementsByClassName('btn-window-close')[0];

        if (windowHeader) {
            /* if present, the header is where you move the DIV from:*/
           windowHeader.onmousedown = dragMouseDown;
        } else {
            /* otherwise, move the DIV from anywhere inside the DIV:*/
            elmnt.onmousedown = dragMouseDown;
        }

        if (closeBtn) {
            closeBtn.onclick = closeWindow;
        }

        function dragMouseDown(e) {
            e = e || window.event;
            // get the mouse cursor position at startup:
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            // call a function whenever the cursor moves:
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            // calculate the new cursor position:
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            // set the element's new position:
            elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
            elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
        }

        function closeDragElement() {
            /* stop moving when mouse button is released:*/
            document.onmouseup = null;
            document.onmousemove = null;
        }

        function closeWindow() {
            elmnt.style.display = "none";

            console.log(flag);
            if (ctlBtn) {
                ctlBtn.style.backgroundColor = 'rgba(57, 152, 156, .7)';
                flag = true;
            }

            console.log(flag);
        }
    }
}