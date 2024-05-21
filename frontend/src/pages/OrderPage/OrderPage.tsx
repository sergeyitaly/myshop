import React, { useState } from 'react';
import axios from 'axios';
import style from './orderpage.module.scss';

interface OrderItem {
    product: string;
    quantity: number;
}

const OrderPage: React.FC = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [address, setAddress] = useState('');
    const [items, setItems] = useState<OrderItem[]>([{ product: '', quantity: 1 }]);

    const handleItemChange = (index: number, field: 'product' | 'quantity', value: string | number) => {
        const newItems = [...items];
        newItems[index][field] = value as never;
        setItems(newItems);
    };

    const addItem = () => {
        setItems([...items, { product: '', quantity: 1 }]);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await axios.post('/api/order/', {
                name,
                email,
                address,
                items,
            });
            alert('Order submitted successfully!');
        } catch (error) {
            console.error('Error submitting order:', error);
        }
    };

    return (
        <div className={style.container}>
            <h1>Place Order</h1>
            <form onSubmit={handleSubmit} className={style.form}>
                <div className={style.formGroup}>
                    <label>Name</label>
                    <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
                </div>
                <div className={style.formGroup}>
                    <label>Email</label>
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
                <div className={style.formGroup}>
                    <label>Address</label>
                    <input type="text" value={address} onChange={(e) => setAddress(e.target.value)} />
                </div>
                <h2>Order Items</h2>
                {items.map((item, index) => (
                    <div key={index} className={style.formGroup}>
                        <label>Product ID</label>
                        <input
                            type="text"
                            value={item.product}
                            onChange={(e) => handleItemChange(index, 'product', e.target.value)}
                        />
                        <label>Quantity</label>
                        <input
                            type="number"
                            value={item.quantity}
                            onChange={(e) => handleItemChange(index, 'quantity', parseInt(e.target.value))}
                        />
                    </div>
                ))}
                <button type="button" onClick={addItem} className={style.addButton}>Add another item</button>
                <button type="submit" className={style.submitButton}>Submit Order</button>
            </form>
        </div>
    );
};

export default OrderPage;
