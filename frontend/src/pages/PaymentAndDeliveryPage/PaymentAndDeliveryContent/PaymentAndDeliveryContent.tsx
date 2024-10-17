import React from 'react';
import { useTranslation } from 'react-i18next';
import { NamedSection } from '../../../components/NamedSection/NamedSection';
import style from './PaymentAndDeliveryContent.module.scss';

interface PaymentAndDeliveryText {
    titleKey: string;
    contentKey: string | { first_paragraph: string; second_paragraph: string };
}

interface PaymentAndDeliveryTextProps {
    sections: PaymentAndDeliveryText[];
}

export const PaymentAndDeliveryContent: React.FC<PaymentAndDeliveryTextProps> = ({ sections }) => {
    const { t } = useTranslation();

    if (!sections) {
        return null;
    }

    return (
        <NamedSection title={t(`payment_and_delivery.title`)} id="payment_and_delivery" className={style.customTitle}>
            <div className={style.container}>
                {sections.map((section, index) => (
                    <div key={index} className={style.section}>
                        <span>{t(`payment_and_delivery.${section.titleKey}`)}</span>
                        {typeof section.contentKey === 'string' ? (
                            <p dangerouslySetInnerHTML={{ __html: t(`payment_and_delivery.${section.contentKey}`) }} className={style.text}/>
                        ) : (
                            <>
                                <p dangerouslySetInnerHTML={{ __html: t(`payment_and_delivery.${section.contentKey.first_paragraph}`) }} className={style.text}/>
                                <p dangerouslySetInnerHTML={{ __html: t(`payment_and_delivery.${section.contentKey.second_paragraph}`) }} className={style.text}/>
                            </>
                        )}
                    </div>
                ))}
            </div>
        </NamedSection>
    );
};
