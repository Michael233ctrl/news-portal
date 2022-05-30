import React from 'react'
import {Card, Row} from "react-bootstrap";
import {Link} from "react-router-dom";

function Post({post}) {
    return (
        <Card className={"my-1"}>
            <Card.Img variant="top" src="holder.js/100px180"/>
            <Card.Body>
                <Link to={`/posts/${post.id}`}>
                    <Card.Text>{post.title}</Card.Text>
                </Link>
            </Card.Body>
        </Card>
    )
}

export default Post