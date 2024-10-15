import React from 'react';
import { useTranslation } from 'react-i18next';
import { NamedSection } from '../../../components/NamedSection/NamedSection';
import style from './PrivacyPolicyContent.module.scss';

interface PrivacyPolicyText {
    titleKey: string;
    contentKey: string | { first_paragraph: string; second_paragraph: string };
}

interface PrivacyPolicyTextProps {
    sections: PrivacyPolicyText[];
}

export const PrivacyPolicyContent: React.FC<PrivacyPolicyTextProps> = ({ sections }) => {
    const { t } = useTranslation();

    if (!sections) {
        return null;
    }

    return (
        <NamedSection title={t(`privacy_and_policy.title`)} id="privacy_and_policy" className={style.customTitle}>
            <div className={style.container}>
                {sections.map((section, index) => (
                    <div key={index} className={style.section}>
                        <span>{t(`privacy_and_policy.${section.titleKey}`)}</span>
                        {typeof section.contentKey === 'string' ? (
                            <p dangerouslySetInnerHTML={{ __html: t(`privacy_and_policy.${section.contentKey}`) }} className={style.text}/>
                        ) : (
                            <>
                                <p dangerouslySetInnerHTML={{ __html: t(`privacy_and_policy.${section.contentKey.first_paragraph}`) }} className={style.text}/>
                                <p dangerouslySetInnerHTML={{ __html: t(`privacy_and_policy.${section.contentKey.second_paragraph}`) }} className={style.text}/>
                            </>
                        )}
                    </div>
                ))}
            </div>
        </NamedSection>
    );
};