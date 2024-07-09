import styled from '@emotion/styled'
import { screen } from '../../constants'

export const PageContainer = styled.div`
    padding-left: clamp(10px, 1vw, 20px);
    padding-right: clamp(10px, 1vw, 20px);
    max-width: ${screen.maxBig};
    margin: 0 auto;

`