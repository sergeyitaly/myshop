import { useTranslation } from "react-i18next";
import { Category, Collection, Currency } from "../models/entities";

export const useAppTranslator = () => {

    const { i18n } = useTranslation();

    const getCategoryName = (category: Category): string => {
        switch (i18n.language) {
            case 'uk':
                return category.name_uk || category.name || '';
            case 'en':
                return category.name_en || category.name || '';
            default:
                return category.name_en || category.name || '';
        }
    };

    const getCollectionName = (collection: Collection): string => {
        switch (i18n.language) {
            case 'uk':
                return collection.name_uk || collection.name || '';
            case 'en':
                return collection.name_en || collection.name || '';
            default:
                return collection.name_en || collection.name || '';
        }
    };

    const getCurrencyFormat = (): Currency => {
        switch (i18n.language) {
            case 'uk':
                return 'UAH';
            case 'en':
                return 'USD';
            case 'fr':
                return 'EUR';
            default:
                return 'USD';
        }
    };

    return {
        i18n,
        getCurrencyFormat,
        getCategoryName,
        getCollectionName
    }
}