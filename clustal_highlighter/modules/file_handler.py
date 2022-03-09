def read_fasta_file(file_path):
    #Reads in a fasta file. Standard stuff
    sequence_dictionary = {}
    sequence = None
    sequence_name = None
    with open(file_path) as f:
        for line in f:
            if '>' in line:
                header = line

                if sequence_name == None:
                    sequence = None
                    sequence_name = header[1:].strip()
                else:
                    sequence_dictionary[sequence_name] = sequence
                    sequence_name = header[1:].strip()
                    sequence = None
            else:
                if sequence == None:
                    sequence = line.strip()
                else:
                    sequence += line.strip() 
    
        sequence_dictionary[sequence_name] = sequence
    return sequence_dictionary

def read_fimo_file(file_path):
    #Reads in a fimo file, standard stuff
    sequence_name_dict = {}
    with open(file_path) as f:
            header = f.readline() #to get rid of it
            for line in f:
                if len(line) <= 1:
                    return sequence_name_dict
                line_split = line.split()
                seq_name = line_split[2]
                start = int(line_split[3])
                stop = int(line_split[4])
                motif_alt_id = line_split[1]

                if seq_name not in sequence_name_dict:
                    sequence_name_dict[seq_name] = []
                    sequence_name_dict[seq_name].append((start, stop, motif_alt_id))
                else:
                    sequence_name_dict[seq_name].append((start, stop, motif_alt_id))  
    return sequence_name_dict

def html_string_to_output(html_string, outputdir):
    #just writes the html string to out
    output = open(outputdir, 'w')
    output.write(html_string)
    output.close

def output_A_seqs(fasta, output, keys):
    #output but with sequences that have A only
    for key in keys:
        seq = fasta[key]
        temp_output_string = ">" + key + "\n"
        for index, char in enumerate(seq):
            if index % 80 == 0 and index > 0:
                temp_output_string += "\n"
                temp_output_string += char
            else:
                temp_output_string += char

        output.write(temp_output_string + '\n\n\n')
    output.close()

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
    });
    </script>
     """
    return html_string