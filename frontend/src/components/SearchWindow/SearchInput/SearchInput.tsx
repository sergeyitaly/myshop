import React, { useState } from 'react';
import { DetailedHTMLProps, InputHTMLAttributes } from 'react';
import { AppIcon } from '../../SvgIconComponents/AppIcon';
import styles from './SearchInput.module.scss';

interface SearchInputProps extends DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement> {
    id: string;
    onClickClose: () => void;
    onSearch: (query: string) => void; // Callback to handle search
}

export const SearchInput = ({
    id,
    onClickClose,
    onSearch,
    ...props
}: SearchInputProps) => {
    const [searchQuery, setSearchQuery] = useState<string>('');

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const query = event.target.value.trim().toLowerCase(); // Normalize to lowercase
        setSearchQuery(query);
        // Call the onSearch callback with the normalized search query
        onSearch(query);
    };

    return (
        <div className={styles.container}>
            <label 
                htmlFor={id}
                className={styles.sign}
            >
                <AppIcon iconName='search'/>
            </label>
            <input 
                id={id}
                autoComplete='off'
                className={styles.input}
                type="text" 
                value={searchQuery}
                onChange={handleInputChange}
                {...props}
            />
            <button onClick={onClickClose}>
                <AppIcon iconName='cross'/>
            </button>
            <span className={styles.underline}/>
        </div>
    );
};
