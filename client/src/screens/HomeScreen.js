import React, {useState, useEffect} from 'react'
import {Card, Row} from "react-bootstrap";

import Post from "../components/Post";
import axios from "axios";

function HomeScreen() {
    const [posts, setPosts] = useState([])

    useEffect(() => {
        async function fetchPosts() {
            const {data} = await axios.get('/api/posts/')
            setPosts(data)
        }

        fetchPosts()
    }, [])
    return (
        <div>
            {posts.map(post => (
                <Row key={post.id} className={"my-3"}>
                    <Post post={post}/>
                </Row>
            ))}
        </div>
    )
}

export default HomeScreen