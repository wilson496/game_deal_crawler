import React from "react"
import WishlistItemRow from "./WishlistItemRow"


type WishListItem = {

    name: string,
    price: number

}

type WishlistState = {

    items: WishListItem[]

}

export default class WishList extends React.Component<{}, WishlistState> {

    componentWillMount() {
        this.setState({
            items: [
                { name: "Valheim", price: 4.99 },
                { name: "Rust", price: 25.13 },
                { name: "My Spicy Booty", price: 3.50 }
            ]
        })
    }

    render() {

        let index = 1
        const rows: JSX.Element[] = []
        for (const item of this.state.items) {
            rows.push(<WishlistItemRow rank={index} name={item.name} price={item.price}/>)
            index = index + 1
        }

        return (
            <div>
                <h1>My Games Wishlist</h1>
                <div>
                    {rows}
                </div>
            </div>
        )

    }

}