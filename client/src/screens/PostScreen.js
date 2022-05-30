import React, {useEffect, useState} from 'react'
import {Row} from "react-bootstrap";
import axios from "axios";
import {Link, useParams} from "react-router-dom";

function PostScreen() {
    let {id} = useParams();

    const [post, setPost] = useState([])
    useEffect(() => {
        async function fetchPosts() {
            const {data} = await axios.get(`/api/posts/${id}`)
            setPost(data)
        }

        fetchPosts()
    }, [])

    return (
        <div>
            <Row>
                <h2>{post.title}</h2>
            </Row>
            <Row>
                <p>
                    {post.text}
                </p>
            </Row>
        </div>
    )
}

export default PostScreen