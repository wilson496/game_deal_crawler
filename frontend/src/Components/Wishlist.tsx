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

    constructor(props: {}) {
        super(props)

        this.state = {
            items: [
                { name: "Valheim", price: 4.99 },
                { name: "Rust", price: 25.13 },
                { name: "My Spicy Booty", price: 3.50 }
            ]
        }
    }

    /**
     * Increases the rank of an item in the list.
     * @param index Index of the item to promote in this.state.items.
     */
    promoteItem(index: number) {
        const items: WishListItem[] = this.state.items.slice()

        // Can't promode an item with index > 1
        if (index > 0) {
            // Swap this element with the one above it
            const toPromote = items[index]
            items[index] = items[index - 1]
            items[index - 1] = toPromote
        }

        this.setState({items: items})
    }

    /**
     * Decreases the rank of an item in the list.
     * @param index Index of the item to demote in this.state.items.
     */
    demoteItem(index: number) {
        const items: WishListItem[] = this.state.items.slice()

        if (index < items.length) {
            // Swap this element with the one below
            const toDemote = items[index]
            items[index] = items[index + 1]
            items[index + 1] = toDemote
        }

        this.setState({items: items})
    }

    render() {

        const rows = this.state.items.map((item, index) => {
            return <WishlistItemRow key={index} rank={index} name={item.name} price={item.price} 
                        promoteItem={() => this.promoteItem(index)}
                        demoteItem={() => this.demoteItem(index)}/>
        })

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