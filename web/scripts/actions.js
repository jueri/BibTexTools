
var bibtexParse = require(['scripts/bibtex_parser.js']);

function update(){
    document.getElementById("output_field").innerHTML = resd;
}

async function getUrl(title) {
    let apiUrl = `https://dblp.org/search/publ/api?q=${title}&format=json`
    let response = await fetch(apiUrl)
    let data = await response.json()
    let url = await data.result.hits.hit[0].url
    return url
  }


function convert(){
    let bibtex_str = document.getElementById("input_field").value;

    let bibtex_parese = bibtexParse.toJSON(bibtex_str);

    for (let i in bibtex_parese) {
        let title = bibtex_parese[i].entryTags.title
        let url = getUrl(title)
        console.log(url)



        // console.log(bibtex_parese[i].entryTags.title)
    };


    // let p = bibtexParse.toJSON('@article{sample1,title={sample title}}');
    // let titles = []
    // for (let i in bibtex_parese) {
    //     titles.push(bibtex_parese[i].entryTags.title)
    //     // console.log(bibtex_parese[i].entryTags.title)
    // };

    // get dblp url

    // await fetch(apiUrl)
    // .then(response => response.json())
    // .then(data => pub_ids.push(data.result.hits.hit[0].url));

    // console.log(pub_ids)

    

    // async function getData(api) {
    //     let response = await fetch(api)
    //     .then(response => response.json())
    //     .then(data => data.result.hits.hit[0].url)
    //     return data;
    // }
    // let a = getData(apiUrl)
    // console.log(a)
    // // .then(data => pub_ids.push(data.result.hits.hit[0].url))
    // // .then(data => console.log(data.result.hits.hit[0].url))

    // console.log("Hi")
    // console.log(pub_ids)
    // console.log(pub_ids[0])



    // let resd = []
    // apiUrl = "https://dblp.org/search/publ/api?q=" + pub_ids[0]
    // console.log(apiUrl)
    // fetch(apiUrl)
    // .then(response => response.json())
    // .then(data => resd.push(data));


    

}