summary_files = [];
counts_files = [];
coverage_files = [];
variant_files = [];

function displayTable(){
    dfd.readCSV(
        summary_files[0]
    ).then((df) => {
        df.plot("table_div").table()
    }).catch((err) => {
        console.log(err);
    })
}

document.getElementById("filepicker").addEventListener(
    "change",
    (event) => {
        for (const file of event.target.files) {
            file_path = file.webkitRelativePath;
            if (file_path.includes('summary')){
                summary_files.push(file);
            } else if (file_path.includes('count')){
                counts_files.push(file);
            } else if (file_path.includes('coverage')){
                coverage_files.push(file);
            } else if (file_path.includes('variant')){
                variant_files.push(file);
            }
        }
        console.log(summary_files);
        console.log(counts_files);
        console.log(coverage_files);
        console.log(variant_files);
        displayTable();
    },
    false
);