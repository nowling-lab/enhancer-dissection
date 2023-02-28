def html_heading():
    """
    HTML boilerplate for html file generations. Includes some CSS and JS to do actions.
    """
    html_string = """
    <!DOCTYPE html>
    <html lang="en-US">
    <head>
        <title>Html Conversion</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="Keywords"
        content="HTML">
        <meta name="Description"
          content="This is a highlighted FIMO output thingy">
          
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <!-- JavaScript Bundle with Popper -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
    <style>
        .variant_hat{
            font-weight: 800;
            font-size: large;
            position: absolute;
            bottom: 0.3rem;
            left: 0;
            right: 0;
            z-index: 1;
        }
        
        .motif{
            position: relative;
            z-index: 2;
        }
        
        pre{
            overflow-x: visible;
            overflow-y: visible;
        }
        
        .has_variant{
            position: relative;
        }
        
        .spacer{
            margin-bottom: 5rem;
        }
        
        #colorbar{
            width: 300px;
            height: 30px;
            outline: auto;
            /* background: linear-gradient(to right,
                                        red 0%,
                                        orange 25%,
                                        yellow 75%,
                                        green 100%); */
            background: linear-gradient(to right,
                                        hsl(54, 98%, 57%) 0%,
                                        hsl(177, 63%, 35%) 50%,
                                        hsl(288, 98%, 17%) 100%);
            vertical-align: middle;
        }   
        
        #colorbar_top_text{
            position: relative;
            margin-left: 25%;
        }
        
        #colorbar_wrapper{
            width: fit-content;
            margin-top: 0.5rem;
        }
        
        #colorbar_with_text{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            width: fit-content;
        }
        
        .heading{
            width: 75%;
        }
        
        .hidden{
            display: none;
        }
        
        body{
            margin-left: 1.5rem;
            background: #D5D8DC;
        }
        
        button{
            margin-top: 1vh;
        }
        
        td {
            padding: 0 15px;
        }
        
        .clear{
        background:#D5D8DC !important;
        }
    """
    return html_string

def highlight_variant_class():
  return """
// Create a class for the element
class HighlightWithVariant extends HTMLElement {
  constructor() {
    // Always call super first in constructor
    super();

    // Create a shadow root
    const shadow = this.attachShadow({mode: 'open'});

    // Wrapper class so tooltips can use position: absolute
    // and z index
    const wrapper = document.createElement('span');
    wrapper.classList.add("wrapper");
    if (typeof this.dataset.motif === 'undefined'){
        wrapper.innerText = "A";
    }

    if (typeof this.dataset.motif !== 'undefined'){
        // Motif highlight
      const motif_data = JSON.parse(this.dataset.motif);
      const motif = document.createElement('span');
      motif.innerText = this.dataset.character;
      motif.classList.add(motif_data.color);
      motif.classList.add("motif");
      wrapper.appendChild(motif);

      // The custom tooltip for this motif
      const motif_popup = document.createElement('span');
      let motif_popup_text = ""
      for (const [key, value] of Object.entries(motif_data)) {
        if (key != 'color'){    
            motif_popup_text += `${key}:
`
            
            for (let motif of value) {
                motif_popup_text += `${motif}
`
            }
        }
       }
      motif_popup.innerHTML = motif_popup_text;
      motif_popup.classList.add("pop-up");
      wrapper.appendChild(motif_popup);
    }

    
    if (typeof this.dataset.variant !== 'undefined'){
      // Variant hat
      const variant_data = JSON.parse(this.dataset.variant);
      const variant = document.createElement('div');
      variant.dataset.ref = variant_data.ref_percent;
      variant.style.color = variant_data.color;
      variant.innerText = "^";
      variant.classList.add("variant");

      wrapper.appendChild(variant);

      // Variant custom tooltip
      const variant_popup = document.createElement('span');
      variant_popup.classList.add("pop-up");
      let variant_text = ""
      variant_text += `Position: ${parseInt(this.dataset.position, 10).toLocaleString("en-US")}\n`
      variant_text += `Ref Allele Percent: ${variant_data.ref_percent}%\n`
      variant_text += `Alt Allele Percent: ${variant_data.alt_percent}%\n`
    //   `
    //   Position: 155 <br>
    //   Ref: 32% <br>
    //   Alt: 68% <br>
    //   Pi Score: 0.351`
      variant_popup.innerHTML = variant_text;
      wrapper.appendChild(variant_popup);
    }

    // Create some CSS to apply to the shadow dom
    const style = document.createElement('style');
    style.textContent = `
      .wrapper {
        position: relative;
      }

      .pop-up {
        font-size: 0.8rem;
        width: 12rem;
        display: inline-block;
        border: 1px solid black;
        padding: 10px;
        background: white;
        border-radius: 10px;
        opacity: 0;
        position: absolute;
        bottom: 20px;
        left: 10px;
        z-index: 1;
      }

      .variant:hover + .pop-up {
        opacity: 1;
        z-index: 4;
      }

      .motif:hover + .pop-up {
        opacity: 1;
        z-index: 4;
      }

      .variant{
        font-weight: 800;
        font-size: large;
        position: absolute;
        bottom: 0.3rem;
        left: 0;
        right: 0;
        z-index: 2;
      }
    
      .motif{
        position: relative;
        z-index: 3;
      }

      .blue{
        background:Aqua;
      }
      
      .purple{
            background:Plum;
      }

      .red{
        background:PaleVioletRed;
      }
    
      .clear{
        background:#D5D8DC !important;
      }
    `;

    // Attach the created elements to the shadow dom
    shadow.appendChild(style);
    shadow.appendChild(wrapper);
    }
}

// Define the new element
customElements.define('highlight-variant', HighlightWithVariant);

function get_spans(className){
    let classNameElements = document.querySelectorAll(`highlight-variant[data-${className}]`);
    let spans = []
    for(let classNameElement of classNameElements){
        highlighted_span = classNameElement.shadowRoot.querySelector(`.motif`);
        spans.push(highlighted_span);
    }
    return spans;
}

function get_variants(){
    let variantHighlights = document.querySelectorAll('highlight-variant[data-variant]');
    let variantDivs = [];
    for (let variantHighlight of variantHighlights){
        variantDivs.push(variantHighlight.shadowRoot.querySelector('div'));
    }
    return variantDivs;
}

let variantDivs = get_variants();
let redSpans = get_spans('red');
let blueSpans = get_spans('blue');
let purpleSpans = get_spans('purple'); 

function toggle_red(){
    redSpans.forEach(function(redSpan){
        redSpan.classList.toggle('red');
    });
    purpleSpans.forEach(function(purpleSpan){
        if (purpleSpan.classList.contains('red') || purpleSpan.classList.length === 1){
            purpleSpan.classList.toggle('red');
        }else{
            purpleSpan.classList.toggle('purple');
            purpleSpan.classList.toggle('blue');  
        }
    });
}

function toggle_blue(){
    blueSpans.forEach(function(blueSpan){
        blueSpan.classList.toggle('blue');
    });
    purpleSpans.forEach(function(purpleSpan){
        if (purpleSpan.classList.contains('blue') || purpleSpan.classList.length === 1){
            purpleSpan.classList.toggle('blue');
        }else{
            purpleSpan.classList.toggle('purple');
            purpleSpan.classList.toggle('red'); 
        }
    });
}

function toggle_variant(){  
    for(let variantDiv of variantDivs){
        if (variantDiv.hidden === true){
            variantDiv.hidden = false;
        }else{
            variantDiv.hidden = true;
        }
    }      
}

document.getElementById('toggle_blue').addEventListener('click', toggle_blue)
document.getElementById('toggle_red').addEventListener('click', toggle_red)
document.getElementById('toggle_variant').addEventListener('click', toggle_variant);
            
const variant_value = document.querySelector("#variant_value");
const variant_input = document.querySelector("#variant_input");
variant_value.textContent = variant_input.value;

variant_input.addEventListener("input", (event) => {
variant_value.textContent = event.target.value;
    for (var variant of variantDivs){
        if (parseFloat(variant.dataset.ref) <= event.target.value){
            variant.hidden = false;
        }else{
            variant.hidden = true;
        }
}    
})
"""