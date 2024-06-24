package com.shakespeare.action.collection;

import org.apache.commons.lang3.StringUtils;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * @author Amos Asa Sue
 * @date 2022/2/24 5:01 下午
 */
public class DateUtils {

    private static final String DATE_FORMAT = "yyyy-MM-dd HH:mm:ss";

    public static Date str2date(String dateStr) throws ParseException {
        if(StringUtils.isBlank(dateStr)){
            return null;
        }
        DateFormat df = new SimpleDateFormat(DATE_FORMAT);
        Date effectiveTime = df.parse(dateStr);
        return effectiveTime;
    }
}
