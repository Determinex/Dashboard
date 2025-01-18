import express, { json } from 'express';
import { get, post } from 'axios';

const app = express();
app.use(json());

app.get('/node/data', async (req, res) => {
    try {
        const response = await get('http://localhost:5000/api/data');
        res.send(response.data);
    } catch (error) {
        res.status(500).send('Error connecting to Flask server');
    }
});

app.post('/node/data', async (req, res) => {
    try {
        const dataToSend = { myData: "Hello from Node.js!" };
        const response = await post('http://localhost:5000/api/data', dataToSend);
        res.send(response.data);
    } catch (error) {
        res.status(500).send('Error connecting to Flask server');
    }
});

app.listen(3000, () => {
    console.log('Node.js server is running on port 3000');
});