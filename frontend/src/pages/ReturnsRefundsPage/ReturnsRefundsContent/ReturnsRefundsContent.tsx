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

    if (!sections) {
        return null;
    }

    return (
        <NamedSection title={t(`returns_refunds`)} id="returns_and_refunds" className={style.customTitle}>
            <div className={style.container}>
                <h2>{t(`returns_and_refunds.title`)}</h2>
                <div className={style.conditions}> 
                    <span>{t(`returns_and_refunds.conditions`)}</span>
                    <a href='http://zakon.rada.gov.ua/cgi-bin/laws/main.cgi?nreg=1023-12' target='_blank'>{t(`returns_and_refunds.law`)}</a>
                </div>
                {sections.map((section, index) => (
                    <div key={index} id={`section_${index}`} className={style.customTitle}>
                        <h2>{t(`returns_and_refunds.${section.titleKey}`)}</h2>
                        <div>
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
                                            <ul>
                                                <li key={idx}>
                                                    {t(`returns_and_refunds.${content}`)}
                                                </li>
                                            </ul>
                                        );
                                    }
                                })
                            ) : (
                                <p className='designation'>{t(`returns_and_refunds.${section.contentKey}`)}</p>
                            )}
                        </div>
                    </div> 
                ))}
                <p className='customParagraph'>{t(`returns_and_refunds.designation`)}</p>
            </div>
        </NamedSection>
    );
};

