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
        let objects = document.querySelectorAll(".bg-gif");

        objects.forEach(btn=>{

            this.addEventListenerAll(btn, e=>{
                let gifIn = btn.dataset.in;
                let gifOut = btn.dataset.out;
                let src = btn.src;
                console.log(src)
                console.log(gifIn)
                
                if (btn.classList.contains('active')) {
                    btn.setAttribute('src', gifOut);
                    btn.removeAttribute('class', 'active');
                }
                else {
                    btn.setAttribute('src', gifIn);
                    btn.setAttribute('class', 'active');
                }

            }, 'drag', 'click');
        });
    };
}

window.animatedIcons = new Controller(); 