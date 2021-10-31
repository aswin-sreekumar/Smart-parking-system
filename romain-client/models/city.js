const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const citySchema = new Schema({
    city: String,
    nLots: Number,
    position: {
        lat: Number,
        lon: Number
    },
    lots: [{
        position: {
            lat: Number,
            lon: Number
        },
        slotid: String,
        totalSlots: Number,
        filledSlots: Number
    }]
});
const City = mongoose.model('City', citySchema);
module.exports = City;