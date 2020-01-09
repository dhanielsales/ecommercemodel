class Controller {

    constructor(){
        this.initEvents();
    }

    addEventListenerAll(element, func, ...events) {
        events.forEach(event => {
        
          element.addEventListener(event, func, false);

        });
    };

    initEvents() {
        let objects = document.querySelectorAll(".btn-gif");

        objects.forEach(btn=>{

            this.addEventListenerAll(btn, e=>{
                let tag = btn.tagName
                if (tag == 'IMG') {
                    let gifIn = btn.dataset.in;
                    let gifOut = btn.dataset.out;
                    let src = btn.src;
                    
                    if (btn.classList.contains('gif-active')) {
                        btn.setAttribute('src', gifOut);
                        btn.classList.remove('gif-active');
                    }
                    else {
                        btn.setAttribute('src', gifIn);
                        btn.classList.add('gif-active');
                    }
                }
                else {
                    let inside = btn.childNodes[1];
                    if (inside.tagName == "IMG") {
                        let gifIn = inside.dataset.in;
                        let gifOut = inside.dataset.out;
                        let src = inside.src;
                        
                        if (inside.classList.contains('gif-active')) {
                            inside.setAttribute('src', gifOut);
                            inside.classList.remove('gif-active');
                        }
                        else {
                            inside.setAttribute('src', gifIn);
                            inside.classList.add('gif-active');
                        }
                    } else { throw new Error("InvalidInternalTag: The inner tag is not a tag <img>."); }
                }
                
            }, 'click');
        });
    };
}

window.animatedIcons = new Controller(); 
