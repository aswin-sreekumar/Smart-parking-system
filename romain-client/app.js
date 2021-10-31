const express = require('express');
const bodyParser = require('body-parser');
require('dotenv').config();
const axios = require('axios');
const request = require('request');
const City = require("./models/city");
const Lot = require("./models/lot");
const mongoose = require('mongoose');
const useragent = require('express-useragent');
const favicon = require('serve-favicon');
const https = require('https');

const app = express();
const uri = process.env.MONGOURL;

mongoose.connect(uri, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    })
    .then((result) => {
        app.listen(process.env.PORT||3000, () => {
            // console.log('Secure server started on port 3000');
        });
    })
    .catch((err) => console.log(err));
const db = mongoose.connection;
db.on("error", console.error.bind(console, "connection error: "));
db.once("open", function () {
    // console.log("Connected successfully");
});
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(express.static(__dirname + '/public'));
app.use(favicon("public/favicon.ico")); 
app.get('/', function (req, res) {
    res.redirect('/home');
});
app.get('/home', function (req, res) {
    var ua = useragent.parse(req.headers['user-agent']);
    if (ua.isMobile) {
        res.render('homem');
    } else {
        res.render('home');
    }
});
app.post('/home', function (req, res) {
    function geocode(address) {
        // console.log(address);
        axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
                params: {
                    address: address,
                    key: process.env.GMAPAPI,
                }
            })
            .then(function (response) {
                res.redirect('/find/' + response.data.results[0].geometry.location.lat + '/' + response.data.results[0].geometry.location.lng);
            })
            .catch(function (error) {
                console.log(error);
            });
    }
    geocode(req.body.addresstocheck);
});
const urlify = (olat, olon, destinations) => {
    var url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=';
    var space = '%2C';
    url += `${olat}`;
    url += space;
    url += `${olon}`;
    url += '&destinations=';
    for (var i = 0; i < destinations.length; i++) {
        url += `${destinations[i].lat}`;
        url += space;
        url += `${destinations[i].lon}`;
        if (i < destinations.length - 1) {
            url += '%7C';
        }
    }
    url += '&key=' + process.env.GMAPAPI;
    return url;
}
app.get('/find/:lat/:long', async function (req, res) {
    City.find().select({
        _id: 0
    }).then((result) => {
        var latf = parseFloat(req.params.lat);
        var lonf = parseFloat(req.params.long);
        // console.log(result);
        var minDis = Infinity;
        var minCity = "";
        var multiplier = 10000;
        for (var i = 0; i < result.length; i++) {
            var city = result[i];
            var lat = city.position.lat;
            var lon = city.position.lon;
            var dis = Math.sqrt(Math.pow(lat - latf, 2) + Math.pow(lon - lonf, 2));
            if (dis < minDis) {
                minDis = dis;
                minCity = city.city;
            }
            // console.log(city);
        }
        // console.log(`minCity : ${minCity}`);
        Lot(minCity).find().then((result2) => {
            // console.log('result2', result2);
            var dists = [];
            for (var i = 0; i < result2.length; i++) {
                var lot = result2[i];
                var lat = lot.position.lat;
                var lon = lot.position.lon;
                // console.log(lat, lon, latf, lonf);
                var dis = Math.sqrt(Math.pow(lat * multiplier - latf * multiplier, 2) + Math.pow(lon * multiplier - lonf * multiplier, 2));
                dists.push({
                    dist: dis,
                    slotid: lot.slotid,
                    lat: lot.position.lat,
                    lon: lot.position.lon,
                    empty: lot.totalslots - lot.filledslots,
                    tot: lot.totalslots
                });
            }
            dists.sort((a, b) => a.dist - b.dist);
            if (dists.length > 10) {
                dists = dists.slice(0, 10);
            }
            // console.log(dists);
            var dmaturl = urlify(latf, lonf, dists);
            request(dmaturl, {
                json: true
            }, (err, resp, body) => {
                if (err) {
                    return console.log(err);
                }
                var dmat = body.rows[0].elements;
                console.log('dmat', dmat);
                var dmat2 = [];
                for (var i = 0; i < dmat.length; i++) {
                    var d = dmat[i];
                    dmat2.push({
                        dist: d.distance.value,
                        slotid: dists[i].slotid,
                        lat: dists[i].lat,
                        lon: dists[i].lon,
                        empty: dists[i].empty,
                        tot: dists[i].tot
                    });
                }
                // console.log(dmat2);
                dmat2.sort((a, b) => a.dist - b.dist);
                var ua = useragent.parse(req.headers['user-agent']);
                if (ua.isMobile) {
                    res.render('findm', {
                        lat: latf,
                        lon: lonf,
                        loclist: dmat2
                    });
                } else {
                    res.render('find', {
                        lat: latf,
                        lon: lonf,
                        loclist: dmat2
                    });
                }
            });
        }).catch((err) => console.log(err));
    }).catch((err) => {
        console.log(err);
    });
});