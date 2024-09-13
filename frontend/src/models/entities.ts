export type Currency = "UAH" | "USD" | "EUR";

export interface AdditionalField {
	name: string;
	value: string;
}

export interface Product {
	id: number;
	collection?: Collection;
	images: ProductImage[];
	photo: string | null;
	photo_tumbnail: string | null;
	photo_url: string | null;
	photo_thumbnail_url: string | null;
	brandimage: string | null;
	name: string;
	name_en?: string;
	name_uk?: string;
	description: string | null;
	price: string;
	discount: string;
	stock: number;
	available: boolean;
	created: Date;
	updated: Date;
	sales_count: number;
	popularity: number;
	slug: string;
	color_name: string | null;
	color_value: string | null;
	size: string | null;
	currency: Currency;
	additional_fields: AdditionalField[];
}

export interface ProductImage {
	id: string;
	images: string;
	images_thumbnail_url: string;
}

export interface Collection {
	id: number;
	category?: Category;
	photo_url: string;
	photo_thumbnail_url: string;
	photo: string;
	name: string;
	name_uk?: string;
	name_en?: string;
	created: Date;
	updated: Date;
	sales_count: number;
}

export interface Category {
	id: number;
	name: string;
	name_uk?: string;
	name_en?: string;
}

export interface User {
	id: number;
	username: string;
	email: string;
}

export interface Color {
	name?: string;
	color: string;
}

export interface ProductVariantsModel {
	colors: Color[];
	sizes: string[];
}

export interface BasketItemModel {
	productId: number;
	qty: number;
}

export interface Order {
	name: string;
	surname: string;
	phone: number;
	email: string;
	address: string;
	receiver: boolean;
	receiver_comments: string | null;
	submitted_at: Date;
}

export interface PriceRange {
	min: number;
	max: number;
}

export interface TeamMember {
	id: number;
	name: string;
	name_en?: string;
	name_uk?: string;
	surname: string;
	surname_en?: string;
	surname_uk?: string;
	description?: string;
	description_en?: string;
	description_uk?: string;
	mobile?: string;
	linkedin?: string;
	link_to_telegram?: string;
	email: string;
	photo?: string;
	photo_thumbnail?: string;
	photo_url: string;
	photo_thumbnail_url: string;
}

export interface Technology {
	id: number;
	name: string;
	name_en?: string;
	name_uk?: string;
	description?: string;
	description_en?: string;
	description_uk?: string;
	link?: string;
	photo?: string;
	photo_thumbnail?: string;
	photo_url: string;
	photo_thumbnail_url: string;
}

export interface Brand {
	id: number;
	name: string;
	name_en?: string;
	name_uk?: string;
	link?: string;
	photo?: string;
	photo_thumbnail?: string;
	photo_url: string;
	photo_thumbnail_url: string;
}
