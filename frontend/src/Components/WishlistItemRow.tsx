import React from "react"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import Button from "react-bootstrap/Button"

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
                <Col sm={7}>
                    {this.props.name}
                    <Button onClick={() => this.props.promoteItem()}>Promote</Button>
                    <Button onClick={() => this.props.demoteItem()}>Demote</Button>
                </Col>
                <Col sm={3}>${this.props.price.toFixed(2)}</Col>
            </Row>
        )
    }

}
