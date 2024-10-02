import style from './style.module.scss'
import {TextField} from "@mui/material";
import { PageContainer } from "../../components/containers/PageContainer"
import {useNavigate} from "react-router-dom";
import {useTranslation} from "react-i18next";
import {useState} from "react";
import axios from "axios";
import {apiBaseUrl} from "../../api/api";


const textFieldStyles = {
    '& .MuiInputLabel-root': {
        fontSize: '24px',
        '@media (max-width:740px)': {
            fontSize: '18px',
        },
    },
    '& .MuiInputBase-root': { height: '50px',
        '@media (max-width:740px)': {
            height: '40px',
        },},
    '& .MuiInputBase-input': { padding: '10px 0' },
};

export const Contact = () => {

    const navigate = useNavigate();
    const { t } = useTranslation();

    const [name, setName] = useState('');
    const [error, setError] = useState(false);
    const [email, setEmail] = useState('');
    const [error2, setError2] = useState(false);
    const [phone_number, setPhone] = useState('');
    const [error3, setError3] = useState(false);
    const [comment, setMessage] = useState('');
    const [error4, setError4] = useState(false);

    const data = {
        name,
        email,
        phone_number,
        comment
    };

    const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;

        if (/\d/.test(value)) {
            setError(true);
        } else {
            setError(false);
        }
        setName(value);
    };

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setEmail(value);

        if (!emailRegex.test(value)) {
            setError2(true);
        } else {
            setError2(false);
        }
    };

    const phoneRegex = /^\+?\d{10,15}$/;

    const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setPhone(value);

        if (!phoneRegex.test(value)) {
            setError3(true);
        } else {
            setError3(false);
        }
    };

    const handleMessageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setMessage(value);
        setError4(value.trim() === '');
    };

    const postComment = async (userData: typeof data) => {
        try {
            const response = await axios.post(`${apiBaseUrl}/api/comments/comments/`, userData);
            console.log('Response:', response.data);
            navigate('/sendcontacts');
        } catch (error) {
            console.error('Error posting comment:', error);
        }
    };

    const handleButtonClick = () => {
        if (!error && !error2 && !error3 && !error4) {
            postComment(data);
        }
    };

    return (
        <PageContainer>
            <div className={style.titleContainer}>
                <p className={style.description}>
                    {t('hello_part_1')}
                    <span className={style.name}> KOLORYT,</span> <br/>
                    {t('hello_part_2')}
                </p>
            </div>
            <div className={style.generalContainer}>
                <div className={style.contactScontainer}>
                    <h3>{t('contacts')}</h3>
                    <p className={style.subTitle}>{t('contact_us')} </p>
                    <p> Instagram </p>
                    <p> Facebook </p>
                    <p className={style.subTitle}>{t('phone')}
                    </p>
                    <p> +380634578932 </p>
                    <p className={style.subTitle}> {t('for_cooperation')} </p>
                    <p> koloryt@gmail.com </p>
                    <p className={style.subTitle}> {t('support')} </p>
                    <p> customer@koloryt.com </p>
                </div>
                <div className={style.formContainer }>
                    <h2> {t('have_question')} </h2>
                    <div className={style.frame}>
                        <TextField
                            id="standard-name"
                            label={t('name')}
                            variant="standard"
                            sx={textFieldStyles}
                            value={name}
                            onChange={handleNameChange}
                            error={error}
                            helperText={error ? t('error_name') : ''}
                        />
                        <TextField
                            label={t('email')}
                            variant="standard"
                            sx={textFieldStyles}
                            value={email}
                            onChange={handleEmailChange}
                            error={error2}
                            helperText={error2 ? t('error_email') : ''}
                            required
                        />
                        <TextField
                            label={t('phone')}
                            variant="standard"
                            sx={textFieldStyles}
                            onChange={handlePhoneChange}
                            value={phone_number}
                            error={error3}
                            helperText={error3 ? t('error_phone') : ''}
                            required
                        />
                        <TextField
                            label={t('message')}
                            variant="standard"
                            sx={textFieldStyles}
                            value={comment}
                            onChange={handleMessageChange}
                            error={error4}
                        />
                        <button className={style.sendButton}
                                onClick={handleButtonClick}
                                disabled={error2 || !email}>
                            {t('send')}
                        </button>
                    </div>
                </div>
            </div>
        </PageContainer>
    );
};
