export interface OrderDTO {
	name: string;
	surname: string;
	phone: string;
	email: string;
	receiver: boolean;
	receiver_comments: string | null;
	present: boolean;
	congrats?: string;
	order_items: {
		product_id: number;
		quantity: number;
	}[];
}
