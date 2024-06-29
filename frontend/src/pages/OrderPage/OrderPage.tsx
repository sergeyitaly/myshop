import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import style from './orderpage.module.scss';
import { Product } from '../../models/entities';

interface OrderItem {
    product_id: string;
    quantity: number;
    price: number;
    product?: Product;
}

const OrderPage: React.FC = () => {
    const [name, setName] = useState('');
    const [surname, setSurname] = useState('');
    const [phone, setPhone] = useState('');
    const [email, setEmail] = useState('');
    const [address, setAddress] = useState('');
    const [receiver, setReceiver] = useState(false);
    const [receiverComments, setReceiverComments] = useState('');
    const [items, setItems] = useState<OrderItem[]>([{ product_id: '', quantity: 1, price: 0 }]);
    const [totalAmount, setTotalAmount] = useState(0);
    const [orderSubmitted, setOrderSubmitted] = useState(false);
    const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;
    const navigate = useNavigate();

    useEffect(() => {
        const calculateTotalAmount = () => {
            const total = items.reduce((acc, item) => acc + item.quantity * item.price, 0);
            setTotalAmount(total);
        };
        calculateTotalAmount();
    }, [items]);

    useEffect(() => {
        if (orderSubmitted) {
            const timer = setTimeout(() => {
                navigate('/');
            }, 2000);
            return () => clearTimeout(timer);
        }
    }, [orderSubmitted, navigate]);

    const handleItemChange = async (index: number, field: 'product_id' | 'quantity' | 'price', value: string | number) => {
        const newItems = [...items];
        newItems[index][field] = value as never;

        if (field === 'product_id' && typeof value === 'string') {
            try {
                const response = await axios.get<Product>(`${apiBaseUrl}/api/product/${value}/`);
                const productData = response.data;
                newItems[index].product = productData;
                newItems[index].price = +productData.price;
            } catch (error) {
                console.error('Error fetching product data:', error);
            }
        }

        setItems(newItems);
    };

    const addItem = () => {
        setItems([...items, { product_id: '', quantity: 1, price: 0 }]);
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
                surname,
                phone,
                email,
                address,
                receiver,
                receiver_comments: receiver ? receiverComments : '',
                order_items: items.map(item => ({
                    product_id: item.product_id,
                    quantity: item.quantity,
                })),
            };

            await axios.post(`${apiBaseUrl}/api/order/`, orderData);
            setOrderSubmitted(true);
            sendEmail();
        } catch (error) {
            console.error('Error submitting order:', error);
        }
    };

    return (
        <div className={style.container}>
            <h1>Place Order</h1>
            {orderSubmitted ? (
                <div className={style.successMessage}>Order has been successfully submitted! Redirecting to home page...</div>
            ) : (
                <form onSubmit={handleSubmit} className={style.form}>
                    <div className={style.formGroup}>
                        <label>Name</label>
                        <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
                    </div>
                    <div className={style.formGroup}>
                        <label>Surname</label>
                        <input type="text" value={surname} onChange={(e) => setSurname(e.target.value)} />
                    </div>
                    <div className={style.formGroup}>
                        <label>Phone</label>
                        <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} />
                    </div>
                    <div className={style.formGroup}>
                        <label>Email</label>
                        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                    </div>
                    <div className={style.formGroup}>
                        <label>Address</label>
                        <input type="text" value={address} onChange={(e) => setAddress(e.target.value)} />
                    </div>
                    <div className={style.formGroup}>
                        <label>
                            <input type="checkbox" checked={receiver} onChange={(e) => setReceiver(e.target.checked)} />
                            Receiver (Other person)
                        </label>
                    </div>
                    {receiver && (
                        <div className={style.formGroup}>
                            <label>Receiver Comments</label>
                            <textarea value={receiverComments} onChange={(e) => setReceiverComments(e.target.value)} />
                        </div>
                    )}
                    <h2>Order Items</h2>
                    {items.map((item, index) => (
                        <div key={index} className={style.formGroup}>
                            <label>Product ID</label>
                            <input
                                type="text"
                                value={item.product_id}
                                onChange={(e) => handleItemChange(index, 'product_id', e.target.value)}
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
                    <div className={style.totalAmount}>Total Amount: ${totalAmount.toFixed(2)}</div>
                    <button type="button" onClick={addItem} className={style.addButton}>Add another item</button>
                    <button type="submit" className={style.submitButton}>Submit Order</button>
                </form>
            )}
        </div>
    );
};

export default OrderPage;
