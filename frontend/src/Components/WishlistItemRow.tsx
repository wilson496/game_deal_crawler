import React from "react"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"

type WishlistItemProps = {

    // Integer indicating rank of the item on the wishlist (1 being highest)
    rank: number

    // Game name
    name: string

    // Decimal number indicating price
    price: number

}

export default class WishlistItemRow extends React.Component<WishlistItemProps> {

    render() { 
        return (
            <Row>
                <Col sm={2} className="text-center">{this.props.rank}</Col>
                <Col sm={7}>{this.props.name}</Col>
                <Col sm={3}>${this.props.price.toFixed(2)}</Col>
            </Row>
        )
    }

}
