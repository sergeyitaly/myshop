import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import style from './orderpage.module.scss';

interface OrderItem {
    product: string;
    quantity: number;
    price: number;
}

interface Product {
    id: string;
    price: number;
}

const OrderPage: React.FC = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [address, setAddress] = useState('');
    const [items, setItems] = useState<OrderItem[]>([{ product: '', quantity: 1, price: 0 }]);
    const [totalAmount, setTotalAmount] = useState(0);
    const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;
    const navigate = useNavigate();

    useEffect(() => {
        calculateTotalAmount();
    }, [items]);

    const handleItemChange = async (index: number, field: 'product' | 'quantity' | 'price', value: string | number) => {
        const newItems = [...items];
        newItems[index][field] = value as never;

        if (field === 'product' && typeof value === 'string') {
            try {
                const response = await axios.get<Product>(`${apiBaseUrl}/api/product/${value}/`);
                newItems[index].price = response.data.price;
            } catch (error) {
                console.error('Error fetching product price:', error);
                newItems[index].price = 0; // Default to 0 if there is an error
            }
        }

        setItems(newItems);
    };

    const addItem = () => {
        setItems([...items, { product: '', quantity: 1, price: 0 }]);
    };

    const calculateTotalAmount = () => {
        const total = items.reduce((acc, item) => acc + item.quantity * item.price, 0);
        setTotalAmount(total);
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
            };

            await axios.post(`${apiBaseUrl}/api/order/`, orderData);
            alert('Order submitted successfully!');
            sendEmail();
            navigate('/');
        } catch (error) {
            console.error('Error submitting order:', error);
        }
    };

    useEffect(() => {
        calculateTotalAmount();
    }, [items]);

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
                        <label>Price</label>
                        <input
                            type="number"
                            value={item.price}
                            readOnly
                        />
                    </div>
                ))}
                <div className={style.totalAmount}>Total Amount: ${totalAmount}</div>
                <button type="button" onClick={addItem} className={style.addButton}>Add another item</button>
                <button type="submit" className={style.submitButton}>Submit Order</button>
            </form>
        </div>
    );
};

export default OrderPage;
