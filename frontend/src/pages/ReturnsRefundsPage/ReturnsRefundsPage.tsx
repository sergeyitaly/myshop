import React from 'react';
import { PageContainer } from '../../components/containers/PageContainer';
import { ReturnsRefundsContent } from './ReturnsRefundsContent/ReturnsRefundsContent';
import { ReturnsRefundsText } from './ReturnsRefundsContent/ReturnsRefundsContent';

const returnsRefundsOptions: ReturnsRefundsText[] = [
    {
        titleKey: 'returns_title',
        contentKey: {
        first_paragraph: 'returns_content.first_paragraph',
        second_paragraph: 'returns_content.second_paragraph',
        third_paragraph: 'returns_content.third_paragraph',
        fourth_paragraph: 'returns_content.fourth_paragraph',
        },
    },
    {
        titleKey: 'refunds_title',
        contentKey: {
        first_option: 'refunds_content.first_option',
        second_option: 'refunds_content.second_option',
        third_option: 'refunds_content.third_option',
        fourth_option: 'refunds_content.fourth_option',
        },
    },
    {
        titleKey: 'terms_title',
        contentKey: {
        first_term: 'terms_content.first_term',
        second_term: 'terms_content.second_term',
        },
    },
];

export const ReturnsRefundsPage: React.FC = () => {
    return (
        <PageContainer>
        <ReturnsRefundsContent sections={returnsRefundsOptions} />
        </PageContainer>
    );
};

export default ReturnsRefundsPage;