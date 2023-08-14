'use strict';

// selectors
const decreaseButtons = document.querySelectorAll('.btn-decrease');
const increaseButtons = document.querySelectorAll('.btn-increase');
const removeFromCartButtons = document.querySelectorAll('.btn-remove');
const totalPriceHeading = document.querySelector('.total-price');

// functionality
function updateCart(action, item_id) {
	if (action === 'remove_from_cart') {
		axios.post(`/${action}/${item_id}`).then((response) => {
			const itemElement = document.getElementById(`cart-item-${item_id}`);

			if (itemElement) {
				itemElement.remove();
			}

			// we fully reload the page only when the last item from the cart has been removed
			if (response.data.cart_length === 0) {
				location.reload();
			}
		});
	} else {
		axios
			.post(`/${action}/${item_id}`)
			.then((response) => {
				// getting updated quantity
				const updatedQuantity = response.data.updated_quantity;

				// getting updated total cart price
				const updatedTotalPrice = response.data.updated_total_price;

				// getting quantity input of particular item
				const quantityInput = document.getElementById(
					`quantity-${item_id}`
				);

				quantityInput.value = updatedQuantity;

				// updating cart total price
				totalPriceHeading.textContent = `£ ${updatedTotalPrice}`;
			})
			.catch((error) => {
				console.error('Error updating cart:', error);
			});
	}
}

// event listeners
document.addEventListener('DOMContentLoaded', () => {
	// event listeners for all decrease quantity buttons
	decreaseButtons.forEach((button) => {
		button.addEventListener('click', () => {
			const item_id = button.dataset.itemId;
			updateCart('decrease_quantity', item_id);
		});
	});

	// event listeners for all increase quantity buttons
	increaseButtons.forEach((button) => {
		button.addEventListener('click', () => {
			const item_id = button.dataset.itemId;
			updateCart('increase_quantity', item_id);
		});
	});

	// event listeners for all remove from cart buttons
	removeFromCartButtons.forEach((button) => {
		button.addEventListener('click', () => {
			const item_id = button.dataset.itemId;
			updateCart('remove_from_cart', item_id);
		});
	});
});
