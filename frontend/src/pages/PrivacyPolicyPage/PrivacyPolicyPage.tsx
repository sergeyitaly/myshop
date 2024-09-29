import React from 'react';
import { PageContainer } from "../../components/containers/PageContainer";
import { PrivacyPolicyContent } from './PrivacyPolicyContent/PrivacyPolicyContent';

const privacyAndPolicyOptions = [
    {
        titleKey: 'privacy_title',
        contentKey: {
            first_paragraph: 'privacy_content.first_paragraph',
            second_paragraph: 'privacy_content.second_paragraph',
        },
    },
    {
        titleKey: 'personal_data_title',
        contentKey: {
            first_paragraph: 'personal_data_content.first_paragraph',
            second_paragraph: 'personal_data_content.second_paragraph',
        },
    },
    {
        titleKey: 'use_data_title',
        contentKey: 'use_data_content',
    },
    {
        titleKey: 'protection_title',
        contentKey: 'protection_content',
    },
    {
        titleKey: 'disclosure_title',
        contentKey: 'disclosure_content',
    },
    {
        titleKey: 'changes_title',
        contentKey: {
            first_paragraph: 'changes_content.first_paragraph',
            second_paragraph: 'changes_content.second_paragraph',
        },
    },
    {
        titleKey: 'contact_title',
        contentKey: 'contact_content',
    }
];

export const PrivacyPolicyPage: React.FC = () => {
    return (
        <PageContainer>
            <PrivacyPolicyContent sections={privacyAndPolicyOptions}/>
        </PageContainer>
    )
};

export default PrivacyPolicyPage;