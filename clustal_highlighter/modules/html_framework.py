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
        
        .clearv2{
            background:#D5D8DC;
        }
        
        .hidden{
            display: none;
        }
        
        body{
            margin-left: 1.5rem;
            background: #D5D8DC;
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