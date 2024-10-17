import React from 'react';
import { PaymentAndDeliveryContent } from './PaymentAndDeliveryContent/PaymentAndDeliveryContent';
import { PageContainer } from "../../components/containers/PageContainer";

const paymentAndDeliveryOptions = [
    {
        titleKey: 'payment_title',
        contentKey: 'payment_content',
    },
    {
        titleKey: 'delivery_title',
        contentKey: 'delivery_content',
    },
    {
        titleKey: 'international_delivery_title',
        contentKey: {
            first_paragraph: 'international_delivery_content.first_paragraph',
            second_paragraph: 'international_delivery_content.second_paragraph',
        },
    },
    {
        titleKey: 'returns_title',
        contentKey: 'returns_content',
    },
    {
        titleKey: 'p_s_title',
        contentKey: 'p_s_content',
    },
];

export const PaymentAndDeliveryPage: React.FC = () => {
    return (
        <PageContainer>
            <PaymentAndDeliveryContent  sections={paymentAndDeliveryOptions}/>
        </PageContainer>
    )
};

export default PaymentAndDeliveryPage;