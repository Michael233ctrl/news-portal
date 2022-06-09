import React from 'react'
import {Card, Col, Image, Row, ListGroup} from "react-bootstrap";
import {LinkContainer} from 'react-router-bootstrap'
import {Link} from "react-router-dom";

function Post({post}) {
    return (
        <Row>
            <Col md={4}>
                <Image src={post.image_file} alt={post.title} fluid/>
            </Col>
            <Col md={8}>
                <ListGroup variant={"flush"}>
                    <ListGroup.Item>
                        <Link to={`/posts/${post.id}`}>
                            <h4>{post.title}</h4>
                        </Link>
                    </ListGroup.Item>
                    <ListGroup.Item>
                        <p>{post.topic}</p>
                    </ListGroup.Item>
                </ListGroup>
            </Col>
        </Row>
    )
}

export default Post