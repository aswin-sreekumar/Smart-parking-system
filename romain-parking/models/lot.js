const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const lotSchema = new Schema({
    position: {
        lat: Number,
        lon: Number
    },
    slotid: String,
    totalslots: Number,
    filledslots: Number
});
module.exports = (cityname) => {
    return mongoose.model('Lot', lotSchema, cityname);
};