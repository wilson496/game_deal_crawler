import React from "react"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import Button from "react-bootstrap/Button"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faArrowCircleUp, faArrowCircleDown } from "@fortawesome/free-solid-svg-icons"

type WishlistItemProps = {

    // Integer indicating rank of the item on the wishlist (1 being highest)
    rank: number

    // Game name
    name: string

    // Decimal number indicating price
    price: number,

    /** Function for promoting an item - func(index) should promote the item. */
    promoteItem: Function

    /** Function for demoting an item - func(index) should demote the item. */
    demoteItem: Function

}

export default class WishlistItemRow extends React.Component<WishlistItemProps> {

    render() { 
        return (
            <Row>
                <Col sm={2} className="text-center">{this.props.rank}</Col>
                <Col sm={1}>
                    <FontAwesomeIcon onClick={() => this.props.promoteItem()} icon={faArrowCircleUp}/>
                    <FontAwesomeIcon onClick={() => this.props.demoteItem()} icon={faArrowCircleDown}/>
                </Col>
                <Col sm={6}>
                    {this.props.name}
                </Col>
                <Col sm={3}>${this.props.price.toFixed(2)}</Col>
            </Row>
        )
    }

}
