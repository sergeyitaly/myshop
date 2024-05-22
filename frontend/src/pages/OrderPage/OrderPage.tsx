import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
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
    const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;
    const navigate = useNavigate(); // Add the useNavigate hook

    const handleItemChange = (index: number, field: 'product' | 'quantity', value: string | number) => {
        const newItems = [...items];
        newItems[index][field] = value as never;
        setItems(newItems);
    };

    const addItem = () => {
        setItems([...items, { product: '', quantity: 1 }]);
    };

    const sendEmail = async () => {
        try {
            await axios.post(`${apiBaseUrl}/api/send-email`, {
                to: email,
                subject: 'Order Confirmation',
                body: `Dear ${name}, \n\nYour order has been successfully submitted. \n\nThank you for shopping with us.`,
            });
            console.log('Email sent successfully!');
        } catch (error) {
            console.error('Error sending email:', error);
        }
    };


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const orderData = {
                name,
                email,
                address,
                items: items.map(item => ({ product: item.product, quantity: item.quantity })),
                // No parent_order_id provided
            };
    
            await axios.post(`${apiBaseUrl}/api/order/`, orderData);
            alert('Order submitted successfully!');
            sendEmail();
            navigate('/');
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
