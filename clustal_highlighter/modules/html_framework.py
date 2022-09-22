def html_heading():
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
        .heading{
            width: 75%;
        }
        .clearv2{
            background:white;
        }
        .hidden{
            display: none;
        }
        body{
            margin-left: 1vw;
        }
        .purple{
            background:Plum;
        }
        button{
            margin-top: 1vh;
        }
        td {
        padding: 0 15px;
        }
    """
    return html_string
    
def html_legend():
    html_string = """
    </head>
    <body>
    <h> Legend: </h>
    
    """
    return html_string()
    
def html_button_js():
    html_string = """
    $(document).ready(function () {   
      $('[data-toggle="tooltip"]').tooltip(); 
            
      $('#toggle_blue').click(function() {
          $( "span.blue" ).toggleClass( "clearv2" );
      });
      
      $('#toggle_red').click(function(){
          $( "span.red" ).toggleClass( "clearv2" );
      });
      
      $('#toggle_purple').click(function(){
          $( "span.purple" ).toggleClass( "clearv2" );
      });
      
      $('#toggle_variant').click(function(){
          $( "span.variant" ).toggleClass( "hidden" );
      });
      
    });
    """

def html_header():
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
        .clear{
            background:white;
        }
        .blue{
            background:Aqua;
        }
        .red{
            background:PaleVioletRed;
        }
        .purple{
            background:Plum;
        }
        .heading{
            width: 75%;
        }
        .clearv2{
            background:white;
        }
        .hidden{
            display: none;
        }
        body{
            margin-left: 1vw;
        }
    </style>
    </head>
    <body>
    <h> Legend: </h>
    <div class = "blue heading"> This is for fimo run with streme.txt as the motif file </div>
    <div class = "red heading"> This is for fimo run with JASPAR as the motif file </div>
    <div class = "purple heading"> This is for when those highlighted motifs overlap </div>
    <div class = "clear" style="width:75%; word-wrap: break-word;"> Colored &#8209;'s indicate that the indel is within a single motif. If they are not colored, then that means the indel is between two of the same (JASPAR or streme) motif </div>
    <span>
    <button id="toggle_blue" type="button" class="btn" style="background:Aqua">Toggle Blue</button>
    <button id="toggle_red" type="button" class="btn" style="background:PaleVioletRed">Toggle Red</button>
    <button id="toggle_purple" type="button" class="btn" style="background:Plum">Toggle Purple</button>
    <button id="toggle_variant" type="button" class="btn btn-secondary">Toggle Variant ^'s</button>
    </span>
    <script type="text/javascript">
    $(document).ready(function () {   
      $('[data-toggle="tooltip"]').tooltip(); 
            
      $('#toggle_blue').click(function() {
          $( "span.blue" ).toggleClass( "clearv2" );
      });
      
      $('#toggle_red').click(function(){
          $( "span.red" ).toggleClass( "clearv2" );
      });
      
      $('#toggle_purple').click(function(){
          $( "span.purple" ).toggleClass( "clearv2" );
      });
      
      $('#toggle_variant').click(function(){
          $( "span.variant" ).toggleClass( "hidden" );
      });
      
    });
    </script>
     """
    return html_string