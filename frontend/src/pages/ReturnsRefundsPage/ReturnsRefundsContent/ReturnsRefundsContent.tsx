import React from 'react';
import { useTranslation } from 'react-i18next';
import { NamedSection } from '../../../components/NamedSection/NamedSection';
import style from './ReturnsRefundsContent.module.scss';

type ContentKey = string | { [key: string]: string };

export interface ReturnsRefundsText {
    titleKey: string;
    contentKey: ContentKey;
}

interface ReturnsRefundsTextProps {
    sections: ReturnsRefundsText[];
}

export const ReturnsRefundsContent: React.FC<ReturnsRefundsTextProps> = ({ sections }) => {
    const { t } = useTranslation();

    return (
        <div className={style.container}>
        {sections.map((section, index) => (
            <NamedSection
            key={index}
            title={t(`returns_and_refunds.${section.titleKey}`)}
            id={`section_${index}`}
            className={style.customTitle}
            >
            <div className={style.customTitle}>
                {typeof section.contentKey === 'object' ? (
                Object.entries(section.contentKey).map(([key, content], idx) => {
                    if (key.includes('paragraph')) {
                    return (
                        <p key={idx} className={style.text}>
                        {idx + 1}. {t(`returns_and_refunds.${content}`)}
                        </p>
                    );
                    } else {
                    return (
                        <li key={idx} className={style.cu}>
                        {t(`returns_and_refunds.${content}`)}
                        </li>
                    );
                    }
                })
                ) : (
                <p>{t(`returns_and_refunds.${section.contentKey}`)}</p>
                )}
            </div>
            </NamedSection>
        ))}
        </div>
    );
};

