
// TED talks

const download = (content, type, fileName) => {
    const blob = new Blob([content], {type : type});
    let a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = fileName;
    a.click();    
};

let content = document.getElementsByClassName(" Grid__cell flx-s:1 p-r:4 ");

let body = [].slice.call(content).reduce((accumulator, currentValue) => {
    return accumulator + currentValue.innerText + "\n\n";
}, "");

let properties = [].slice.call(document.getElementsByTagName('meta')).filter((i) => {
    return i.hasAttribute('itemprop') ? i.attributes.itemprop.nodeValue == "name" : false;
});

let jsonObj = {
    author: properties[1].content,
    body: body,
    title: properties[0].content,
    type: "video",
    url: document.URL
};

download(
    JSON.stringify(jsonObj, null, 2),
    'application/json',
    jsonObj.title.toLowerCase().split(' ').join('_').concat('.json')
);

// Olhar digital

const download = (content, type, fileName) => {
    const blob = new Blob([content], {type : type});
    let a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = fileName;
    a.click();    
};

let jsonObj = {
    author: decodeURIComponent(escape(document.getElementsByClassName("meta-item meta-aut")[0].innerText)),
    body: document.getElementsByClassName("mat-txt")[0].innerText,
    title: document.getElementsByClassName("mat-tit")[0].innerText,
    type: "article",
    url: document.URL
};

download(
    JSON.stringify(jsonObj, null, 2),
    'application/json',
    jsonObj.title.toLowerCase().split(' ').join('_').concat('.json')
);


// StartSe

const download = (content, type, fileName) => {
    const blob = new Blob([content], {type : type});
    let a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = fileName;
    a.click();    
};

let content = document.getElementsByClassName("content-single__sidebar-content__content")[0].childNodes;

let filteredContent = [].slice.call(content).filter((i) => {
    return i.tagName == 'P';
});

let body = filteredContent.reduce((accumulator, currentValue) => {
    return accumulator + currentValue.innerText + "\n\n";
}, "");


let jsonObj = {
    author: document.getElementsByClassName("title-single__info__author__about__name")[0].childNodes[1].innerText,
    body: body,
    title: document.getElementsByClassName("title-single__title__name")[0].innerText,
    type: "article",
    url: document.URL
};


download(
    JSON.stringify(jsonObj, null, 2),
    'application/json',
    jsonObj.title.toLowerCase().split(' ').join('_').concat('.json')
);