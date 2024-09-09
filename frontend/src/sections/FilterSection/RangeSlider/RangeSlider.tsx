import { Slider } from '@mui/material';
import { ChangeEvent, useEffect } from 'react';
import styles from './RangeSlider.module.scss'
import { formatPrice } from '../../../functions/formatPrice';
import { formatNumber } from '../../../functions/formatNumber';
import { useDebounce } from '../../../hooks/useDebounce';


interface AppRangeSliderPeops {
    value: [number, number]
    minValue: number
    maxValue: number
    changePrice: (priceRange: [number, number]) => void
}

export const AppRangeSlider = ({
    value,
    minValue,
    maxValue,
    changePrice
}: AppRangeSliderPeops) => {

    const minDistance = 1000;

    console.log(value);

    const value1 = useDebounce(value[0].toString(), 500)
    const value2 = useDebounce(value[1].toString(), 500)
    
    useEffect(() => {
        if(+value1 > value[1]){
            changePrice([value[1], value[1]])
        }
    }, [value1])
   
    useEffect(() => {
        if(+value2 < value[0]){
            changePrice([value[0], value[0]])
        }
    }, [value2])
    

    const handleChange2 = (
      _: Event,
      newValue: number | number[],
      activeThumb: number,
    ) => {
        
      if (!Array.isArray(newValue)) {
        return;
      }
  
      if (newValue[1] - newValue[0] < minDistance) {
        if (activeThumb === 0) {
          const clamped = Math.min(newValue[0],maxValue - minDistance);
          changePrice([clamped, clamped + minDistance]);
        } else {
          const clamped = Math.max(newValue[1], minDistance);
          changePrice([clamped - minDistance, clamped]);
        }
      } else {
        changePrice(newValue as [number, number]);
      }
    };

    const handleChangeInp1 = (e: ChangeEvent<HTMLInputElement>) => {
        let transformedValue = parseFloat(e.target.value.replace(/\s/g, '').replace(/,/g, '.'))
        if(!e.target.value){
            transformedValue = 0
        }
        
        if(!isNaN(+transformedValue) && transformedValue <= maxValue){
            changePrice([transformedValue, value[1]])
        }
    }

    const handleChangeInp2 = (e: ChangeEvent<HTMLInputElement>) => {
        let transformedValue = parseFloat(e.target.value.replace(/\s/g, '').replace(/,/g, '.'))
        if(!e.target.value){
            transformedValue = 0
        }
        if(!isNaN(+transformedValue) && transformedValue <= maxValue){
            changePrice([value[0], transformedValue])
        }
    }

    return (
        <div className={styles.appSlider}>
            <Slider
                getAriaLabel={() => 'Minimum distance shift'}
                value={value}
                onChange={handleChange2}
                disableSwap
                min = {minValue}
                max = {maxValue}
                classes={{
                    thumb: styles.thumb,
                    active: styles.active,
                    rail: styles.rail,
                    track: styles.track
                }}
            />
            <div className={styles.priceRange}>
                <span>{formatPrice(value[0], 'UAH') }</span>
                <span>{formatPrice(value[1], 'UAH')}</span>
            </div>
            <div className={styles.inputContainer}>
                <input 
                    type="text" 
                    value={formatNumber(value[0], 0) }
                    onChange={handleChangeInp1}
                />
                <input 
                    type="text" 
                    value={formatNumber(value[1], 0)}
                    onChange={handleChangeInp2}
                />
            </div>
        </div>
    )
}