const express = require('express');
const router = express.Router();
const pool =  require('../config/db.js');


router.get('/', (req, res) => {
    res.send(form.jsx)
  }) 

  router.get('/users', async (req, res) => {
    pool.getConnection( (err, conn) => {
        if (err) throw err;

        try {
            const qry = 'SELECT u.firstname, u.lastname, u.department FROM users';
            conn.query(qry, (err, result) => {
                conn.release();
                if (err) throw err;
                res.send(JSON.stringify(result));
            });
        } catch (err) {
            console.log(err);
            res.end();
        }
    });
});
/*
router.post('/addTweet', async (req, res) => {
    const userTweet = req.body.tweetInput;
    const userId = 1; // 1=codrkai, 2=eaglefang

    pool.getConnection( (err, conn) => {
        if (err) throw err;

        const qry = `INSERT INTO tweets(tweet, user_id) VALUES(?,?)`;
        conn.query(qry, [userTweet, userId], (err, result) => {
            conn.release();
            if (err) throw err;
            console.log('Tweet added!');
        });

        res.redirect('/tweets');
        res.end();
    });
});
*/
module.exports = router;