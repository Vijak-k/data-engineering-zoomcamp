with trip_unioned as (
    select * from {{ ref('int_trips_unioned') }}
),

vendors as (
    select
        distinct vendor_id,
        {{ get_vendor_name('vendor_id') }} as vendor_name
    from trip_unioned
)

select * from vendors